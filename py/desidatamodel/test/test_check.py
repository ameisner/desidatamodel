# Licensed under a 3-clause BSD style license - see LICENSE.rst
# -*- coding: utf-8 -*-
"""Test desidatamodel.check functions
"""
import os
import sys
import unittest
from unittest.mock import patch
from pkg_resources import resource_filename

from .datamodeltestcase import DataModelTestCase, DM

from .. import DataModelError
from ..check import (DataModel, collect_files, files_to_regexp, scan_model,
                     validate_prototypes, log, _options)


class TestCheck(DataModelTestCase):

    def test_scan_model(self):
        """Test identification of data model files.
        """
        root = os.path.join(os.environ[DM], 'doc', 'examples')
        files = scan_model(root)
        expected = set([os.path.join(root, f) for f in ('badModel.rst',
                                                        'sdR.rst',
                                                        'spPlate.rst')])
        found = set([p.filename for p in files])
        self.assertEqual(expected, found)

    def test_files_to_regexp(self):
        """Test compilation of regular expressions.
        """
        root = os.path.join(os.environ[DM], 'doc', 'DESI_SPECTRO_DATA')
        files = scan_model(root)
        files_to_regexp('/desi/spectro/data', files)
        regexps = ['/desi/spectro/data/20160703/12345678/coordinates-12345678.fits',
                   '/desi/spectro/data/20160703/12345678/desi-12345678.fits.fz',
                   '/desi/spectro/data/20160703/12345678/fiberassign-12345678.fits.gz',
                   '/desi/spectro/data/20160703/12345678/fibermap-12345678.fits',
                   '/desi/spectro/data/20160703/00000123/focus-00000123.fits.fz',
                   '/desi/spectro/data/20160703/00000123/fvc-00000123.fits.fz',
                   '/desi/spectro/data/20160703/00000123/guide-00000123.fits.fz',
                   '/desi/spectro/data/20160703/00000123/guide-rois-00000123.fits.fz',
                   '/desi/spectro/data/20160703/00000123/pm-00000123.fits',
                   '/desi/spectro/data/20160703/00000123/sky-00000123.fits.fz',]
        expected = [os.path.join(root, 'NIGHT', 'EXPID', f) for f in (
            'coordinates-EXPID.rst',
            'desi-EXPID.rst',
            'fiberassign-EXPID.rst',
            'fibermap-EXPID.rst',
            'focus-EXPID.rst',
            'fvc-EXPID.rst',
            'guide-EXPID.rst',
            'guide-rois-EXPID.rst',
            'pm-EXPID.rst',
            'sky-EXPID.rst',)]
        expected_f2r = dict(zip(expected, regexps))
        for f in files:
            self.assertRegex(expected_f2r[f.filename], f.regexp,
                             ("{0} does not " +
                              "match {1}").format(f.regexp.pattern,
                                                  expected_f2r[f.filename]))

    def test_collect_files(self):
        """Test finding files that correspond to data model files.
        """
        test_files = (os.path.join(self.data_dir, 'sdR-12345678.fits'),
                      os.path.join(self.data_dir, 'sdR-01234567.fits'),
                      os.path.join(self.data_dir, 'spPlate-1234-54321.fits'),
                      os.path.join(self.data_dir, 'extraneous.fits'))
        for f in test_files:
            open(f, 'a').close()
        root = os.path.join(os.environ[DM], 'doc', 'examples')
        files = scan_model(root)
        files_to_regexp(self.data_dir, files)

        self.assertInLog(log, ("{0}/doc/examples/badModel.rst has no file " +
                               "regexp!").format(os.environ[DM]))
        collect_files(self.data_dir, files)
        self.assertInLog(log, 'Extraneous file detected: {0}'.format(test_files[3]))
        for f in files:
            if os.path.basename(f.filename) == 'badModel.rst':
                self.assertIsNone(f.regexp)
                self.assertIsNone(f.prototype)
            else:
                self.assertIsNotNone(f.regexp)
                self.assertIsNotNone(f.prototype)
        for f in test_files:
            os.remove(f)

    def test_collect_files_missing(self):
        """Test finding files when some are missing.
        """
        test_files = (os.path.join(self.data_dir, 'sdR-12345678.fits'),
                      os.path.join(self.data_dir, 'sdR-01234567.fits'))
        for f in test_files:
            open(f, 'a').close()
        root = os.path.join(os.environ[DM], 'doc', 'examples')
        files = scan_model(root)
        files_to_regexp(self.data_dir, files)

        self.assertInLog(log, ("{0}/doc/examples/badModel.rst has no file " +
                               "regexp!").format(os.environ[DM]))
        collect_files(self.data_dir, files)
        self.assertInLog(log, ('No files found matching {0}/doc/examples/' +
                               'spPlate.rst!').format(os.environ[DM]))
        for f in test_files:
            os.remove(f)

    def test_extract_metadata(self):
        """Test reading metadata from data model files.
        """
        ex_meta = {'PRIMARY':
                   {'title': 'HDU0',
                    'number': 0,
                    'extension': 'IMAGE',
                    'extname': 'PRIMARY',
                    'format': 'Data: FITS image [int16, 100x100]',
                    'keywords': [('NAXIS1', '100', 'int', ''),
                                 ('NAXIS2', '100', 'int', ''),
                                 ('BSCALE', '1', 'int', ''),
                                 ('BZERO', '32768', 'int',
                                  'Data are really unsigned 16-bit int.'),
                                 ('EXTNAME', 'PRIMARY', 'str', '')]},
                   'Galaxies':
                   {'title': 'HDU1',
                    'number': 1,
                    'extension': 'BINTABLE',
                    'extname': 'Galaxies',
                    'format': [('target', 'char[20]', '', ''),
                               ('V_mag', 'float32', 'mag', ''),
                               ('vdisp',  'float64',  'km/s', '')],
                    'keywords': [('NAXIS1', '32', 'int',
                                  'length of dimension 1'),
                                 ('NAXIS2', '3', 'int',
                                  'length of dimension 2')]}}
        modelfile = resource_filename('desidatamodel.test', 't/fits_file.rst')
        model = DataModel(modelfile, os.path.dirname(modelfile))
        meta = model.extract_metadata()
        self.assertEqual(len(meta.keys()), len(ex_meta.keys()))
        for key, m in meta.items():
            self.assertEqual(m['title'], ex_meta[key]['title'])
            self.assertEqual(m['number'], ex_meta[key]['number'])
            self.assertEqual(m['extension'], ex_meta[key]['extension'])
            self.assertEqual(m['extname'], ex_meta[key]['extname'])
            for k in range(len(m['keywords'])):
                self.assertEqual(m['keywords'][k], ex_meta[key]['keywords'][k])
            if m['extension'] == "IMAGE":
                self.assertEqual(m['format'], ex_meta[key]['format'])
            else:
                for k in range(len(m['format'])):
                    self.assertEqual(m['format'][k], ex_meta[key]['format'][k])

    def test_extract_metadata_missing_extname(self):
        """Test reading metadata with missing EXTNAME.
        """
        modelfile = resource_filename('desidatamodel.test', 't/fits_file.rst')
        model = DataModel(modelfile, os.path.dirname(modelfile))
        meta = model.extract_metadata()
        lines = model._metafile_data.split('\n')
        lines[53] = ''
        model._metafile_data = '\n'.join(lines) + '\n'
        with self.assertRaises(DataModelError) as e:
            meta = model.extract_metadata(error=True)
        self.assertEqual(str(e.exception), "HDU 1 in {0} has no EXTNAME!".format(modelfile))
        meta = model.extract_metadata(error=False)
        self.assertLog(log, -1, "HDU 1 in {0} has no EXTNAME!".format(modelfile))

    def test_extract_metadata_bad_keyword_unit(self):
        """Test reading metadata with bad FITS BUNIT values.
        """
        erg_msg = self.badUnitMessage('ergs')
        modelfile = resource_filename('desidatamodel.test', 't/fits_file.rst')
        model = DataModel(modelfile, os.path.dirname(modelfile))
        meta = model.extract_metadata()
        lines = model._metafile_data.split('\n')
        lines.insert(46, "BUNIT  ergs          str  This is a bad unit.")
        model._metafile_data = '\n'.join(lines) + '\n'
        with self.assertRaises(ValueError) as e:
            meta = model.extract_metadata(error=True)
        self.assertEqual(str(e.exception), erg_msg)
        meta = model.extract_metadata(error=False)
        self.assertLog(log, -1, "HDU 0 in {0} should have a more meaningful EXTNAME than 'PRIMARY'.".format(modelfile))
        self.assertLog(log, -2, erg_msg)

    def test_extract_metadata_missing_keyword_unit(self):
        """Test reading metadata with missing units for header keywords.
        """
        modelfile = resource_filename('desidatamodel.test', 't/fits_file.rst')
        model = DataModel(modelfile, os.path.dirname(modelfile))
        meta = model.extract_metadata()
        lines = model._metafile_data.split('\n')
        lines.insert(46, "BUNIT  erg                This is a bad unit.")
        model._metafile_data = '\n'.join(lines) + '\n'
        with self.assertRaises(DataModelError) as e:
            meta = model.extract_metadata(error=True)
        self.assertEqual(str(e.exception), "Missing type for keyword BUNIT in HDU 0 of {0}!".format(modelfile))
        meta = model.extract_metadata(error=False)
        self.assertLog(log, -1, "HDU 0 in {0} should have a more meaningful EXTNAME than 'PRIMARY'.".format(modelfile))
        self.assertLog(log, -2, "Missing type for keyword BUNIT in HDU 0 of {0}!".format(modelfile))

    def test_extract_metadata_bad_column_unit(self):
        """Test reading metadata with bad FITS column units.
        """
        erg_msg = self.badUnitMessage('ergs')
        modelfile = resource_filename('desidatamodel.test', 't/fits_file.rst')
        model = DataModel(modelfile, os.path.dirname(modelfile))
        meta = model.extract_metadata()
        lines = model._metafile_data.split('\n')
        lines[75] = 'vdisp  float64  ergs'
        model._metafile_data = '\n'.join(lines) + '\n'
        with self.assertRaises(ValueError) as e:
            meta = model.extract_metadata(error=True)
        self.assertEqual(str(e.exception), erg_msg)
        meta = model.extract_metadata(error=False)
        self.assertLog(log, -1, erg_msg)

    def test_extract_metadata_missing_column_type(self):
        """Test reading metadata with missing FITS column types.
        """
        modelfile = resource_filename('desidatamodel.test', 't/fits_file.rst')
        model = DataModel(modelfile, os.path.dirname(modelfile))
        meta = model.extract_metadata()
        lines = model._metafile_data.split('\n')
        lines[75] = 'vdisp'
        model._metafile_data = '\n'.join(lines) + '\n'
        with self.assertRaises(DataModelError) as e:
            meta = model.extract_metadata(error=True)
        self.assertEqual(str(e.exception), "Missing type for column vdisp in HDU 1 of {0}!".format(modelfile))
        meta = model.extract_metadata(error=False)
        self.assertLog(log, -1, "Missing type for column vdisp in HDU 1 of {0}!".format(modelfile))

    def test_validate_prototypes(self):
        """Test the data model validation function.
        """
        modelfile = resource_filename('desidatamodel.test', 't/fits_file.rst')
        f = DataModel(modelfile, os.path.dirname(modelfile))
        f.get_regexp(os.path.dirname(modelfile))
        collect_files(os.path.dirname(modelfile), [f])
        validate_prototypes([f])

    def test_validate_prototype_no_prototype(self):
        """Test the data model validation method with no prototype.
        """
        modelfile = resource_filename('desidatamodel.test', 't/fits_file.rst')
        f = DataModel(modelfile, os.path.dirname(modelfile))
        f.get_regexp(os.path.dirname(modelfile))
        collect_files(os.path.dirname(modelfile), [f])
        f.prototype = None
        f.validate_prototype(error=True)

    def test_validate_prototype_hdu_mismatch(self):
        """Test the data model validation method with wrong number of HDUs.
        """
        modelfile = resource_filename('desidatamodel.test', 't/fits_file.rst')
        f = DataModel(modelfile, os.path.dirname(modelfile))
        f.get_regexp(os.path.dirname(modelfile))
        collect_files(os.path.dirname(modelfile), [f])
        f.validate_prototype()
        f._stub.nhdr = 3
        f.validate_prototype(error=True)
        self.assertLog(log, -1, "Prototype file {0} has the wrong number of sections (HDUs) according to {1}.".format(modelfile.replace('.rst', '.fits'), modelfile))

    def test_validate_prototype_hdu_keyword_mismatch(self):
        """Test the data model validation method with wrong number of HDU keywords.
        """
        modelfile = resource_filename('desidatamodel.test', 't/fits_file.rst')
        f = DataModel(modelfile, os.path.dirname(modelfile))
        f.get_regexp(os.path.dirname(modelfile))
        collect_files(os.path.dirname(modelfile), [f])
        f.validate_prototype()
        f._stub_meta[0]['keywords'].append(('BUNIT', 'erg', 'str', 'This is a test.'))
        f.validate_prototype(error=True)
        self.assertLog(log, -1, "File {0} HDU0 extra keywords according to {1}: {{'BUNIT'}}".format(modelfile.replace('.rst', '.fits'), modelfile))

    def test_validate_prototype_hdu_wrong_keyword(self):
        """Test the data model validation method with wrong HDU keyword names.
        """
        modelfile = resource_filename('desidatamodel.test', 't/fits_file.rst')
        f = DataModel(modelfile, os.path.dirname(modelfile))
        f.get_regexp(os.path.dirname(modelfile))
        collect_files(os.path.dirname(modelfile), [f])
        f.validate_prototype()
        f._stub_meta[0]['keywords'][-1] = ('BUNIT', 'erg', 'str', 'This is a test.')
        f.validate_prototype(error=True)
        self.assertLog(log, -2, "File {0} HDU0 missing keywords according to {1}: {{'BZERO'}}".format(modelfile.replace('.rst', '.fits'), modelfile))
        self.assertLog(log, -1, "File {0} HDU0 extra keywords according to {1}: {{'BUNIT'}}".format(modelfile.replace('.rst', '.fits'), modelfile))

    def test_validate_prototype_hdu_extension_type(self):
        """Test the data model validation method with wrong HDU extension type.
        """
        modelfile = resource_filename('desidatamodel.test', 't/fits_file.rst')
        f = DataModel(modelfile, os.path.dirname(modelfile))
        f.get_regexp(os.path.dirname(modelfile))
        collect_files(os.path.dirname(modelfile), [f])
        f.validate_prototype()
        f._stub_meta[1]['extension'] = 'IMAGE'
        f.validate_prototype(error=True)
        self.assertLog(log, -1, "Prototype file {0} has an extension type mismatch in HDU1 (IMAGE != BINTABLE) according to {1}.".format(modelfile.replace('.rst', '.fits'), modelfile))
        # f._stub_meta[1]['extname'] = ''
        # f.validate_prototype(error=True)
        # self.assertLog(log, -1, "Prototype file {0} has no EXTNAME in HDU1.".format(modelfile.replace('.rst', '.fits')))

    def test_validate_prototype_hdu_extension_name(self):
        """Test the data model validation method with wrong HDU extension name.
        """
        modelfile = resource_filename('desidatamodel.test', 't/fits_file.rst')
        f = DataModel(modelfile, os.path.dirname(modelfile))
        f.get_regexp(os.path.dirname(modelfile))
        collect_files(os.path.dirname(modelfile), [f])
        f.validate_prototype()
        f._stub_meta[1]['extname'] = 'GALAXY'
        f.validate_prototype(error=True)
        self.assertLog(log, -1, "Prototype file {0} has an EXTNAME mismatch in HDU1 (GALAXY != Galaxies) according to {1}.".format(modelfile.replace('.rst', '.fits'), modelfile))
        f._stub_meta[1]['extname'] = ''
        f.validate_prototype(error=True)
        self.assertLog(log, -2, "Prototype file {0} has no EXTNAME in HDU1.".format(modelfile.replace('.rst', '.fits')))
        self.assertLog(log, -1, "Could not find EXTNAME = '' in {0}; trying by HDU number.".format(modelfile))

    def test_extract_columns(self):
        """Test extraction of columns from a row of data.
        """
        modelfile = resource_filename('desidatamodel.test', 't/fits_file.rst')
        f = DataModel(modelfile, os.path.dirname(modelfile))
        foo = '======= ============= ==== ====================='
        columns = list(map(len, foo.split()))
        row = 'NAXIS1  32            int  length of dimension 1'
        exc = ('NAXIS1', '32', 'int', 'length of dimension 1')
        c = f._extract_columns(row, columns)
        self.assertEqual(c, exc)

    def test_cross_reference(self):
        """Test parsing of cross-references.
        """
        modelfile = resource_filename('desidatamodel.test', 't/fits_file.rst')
        f = DataModel(modelfile, os.path.dirname(modelfile))
        line = "See :doc:`Other file <fits_file>`"
        ref = f._cross_reference(line)
        self.assertEqual(ref, resource_filename('desidatamodel.test',
                                                't/fits_file.rst'))

    @patch('sys.argv', ['check_model', '--verbose', '--compare-files', 'DESI_SPECTRO_DATA', '/desi/spectro/data/desi-00000000.fits.fz'])
    def test_options(self):
        """Test parse of command-line options.
        """
        options = _options()
        self.assertTrue(options.verbose)
        self.assertTrue(options.files)
        self.assertEqual(options.section, 'DESI_SPECTRO_DATA')
        self.assertEqual(options.directory, '/desi/spectro/data/desi-00000000.fits.fz')


def test_suite():
    """Allows testing of only this module with the command::

        python setup.py test -m <modulename>
    """
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
