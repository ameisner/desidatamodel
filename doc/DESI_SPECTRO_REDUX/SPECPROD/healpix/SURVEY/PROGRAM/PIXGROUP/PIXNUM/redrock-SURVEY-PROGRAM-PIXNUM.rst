==================================
redrock-SURVEY-PROGRAM-PIXNUM.fits
==================================

:Summary: *This section should be filled in with a high-level description of
    this file. In general, you should remove or replace the emphasized text
    (\*this text is emphasized\*) in this document.*
:Naming Convention: ``redrock-SURVEY-PROGRAM-PIXNUM.fits``, where ``SURVEY`` is
    *e.g.* ``main`` or ``sv1``, ``PROGRAM`` is *e.g.* ``bright or ``dark``
    and ``PIXNUM`` is the HEALPixel number.
:Regex: ``redrock-(main|sv1|sv2|sv3)-(backup|bright|dark|other)-[0-9]+\.fits``
:File Type: FITS, 354 KB

Contents
========

====== ============ ======== ===================
Number EXTNAME      Type     Contents
====== ============ ======== ===================
HDU0_               IMAGE    Empty
HDU1_  REDSHIFTS    BINTABLE Table with best fit redshifts
HDU2_  FIBERMAP     BINTABLE Propagated fibermap file data
HDU3_  EXP_FIBERMAP BINTABLE *Brief Description*
HDU4_  TSNR2        BINTABLE *Brief Description*
====== ============ ======== ===================


FITS Header Units
=================

HDU0
----

Required Header Keywords
~~~~~~~~~~~~~~~~~~~~~~~~

======== ============= ==== ===============
KEY      Example Value Type Comment
======== ============= ==== ===============
RRVER    0.15.0        str  Redrock version
TEMNAM00 GALAXY        str
TEMVER00 2.6           str
TEMNAM01 QSO           str
TEMVER01 0.1           str
TEMNAM02 STAR:::A      str
TEMVER02 0.1           str
TEMNAM03 STAR:::B      str
TEMVER03 0.1           str
TEMNAM04 STAR:::CV     str
TEMVER04 0.1           str
TEMNAM05 STAR:::F      str
TEMVER05 0.1           str
TEMNAM06 STAR:::G      str
TEMVER06 0.1           str
TEMNAM07 STAR:::K      str
TEMVER07 0.1           str
TEMNAM08 STAR:::M      str
TEMVER08 0.1           str
TEMNAM09 STAR:::WD     str
TEMVER09 0.1           str
======== ============= ==== ===============

Empty HDU.

HDU1
----

EXTNAME = REDSHIFTS

*Summarize the contents of this HDU.*

Required Header Keywords
~~~~~~~~~~~~~~~~~~~~~~~~

====== ============= ==== =====================
KEY    Example Value Type Comment
====== ============= ==== =====================
NAXIS1 170           int  length of dimension 1
NAXIS2 415           int  length of dimension 2
====== ============= ==== =====================

Required Data Table Columns
~~~~~~~~~~~~~~~~~~~~~~~~~~~

========= =========== ===== ===========
Name      Type        Units Description
========= =========== ===== ===========
TARGETID  int64             Target ID for this row
CHI2      float64           Best fit :math:`\chi^2`
COEFF     float64[10]       Redrock template coefficients
Z         float64           Best fit redshift
ZERR      float64           Uncertainty on best fit redshift
ZWARN     int64             Warning flags; 0 is good
NPIXELS   int64
SPECTYPE  char[6]           Spectral type
SUBTYPE   char[20]          Spectral subtype (maybe blank)
NCOEFF    int64
DELTACHI2 float64           :math:`\Delta \chi^2` to next best fit
========= =========== ===== ===========

HDU2
----

EXTNAME = FIBERMAP

*Summarize the contents of this HDU.*

Required Header Keywords
~~~~~~~~~~~~~~~~~~~~~~~~

====== ============= ==== =====================
KEY    Example Value Type Comment
====== ============= ==== =====================
NAXIS1 317           int  length of dimension 1
NAXIS2 415           int  length of dimension 2
====== ============= ==== =====================

Required Data Table Columns
~~~~~~~~~~~~~~~~~~~~~~~~~~~

========================== ======= ===== ===========
Name                       Type    Units Description
========================== ======= ===== ===========
TARGETID                   int64
COADD_FIBERSTATUS          int32
TARGET_RA                  float64
TARGET_DEC                 float64
PMRA                       float32
PMDEC                      float32
REF_EPOCH                  float32
FA_TARGET                  int64
FA_TYPE                    binary
OBJTYPE                    char[3]
SUBPRIORITY                float64
OBSCONDITIONS              int32
RELEASE                    int16
BRICKID                    int32
BRICK_OBJID                int32
MORPHTYPE                  char[4]
FLUX_G                     float32
FLUX_R                     float32
FLUX_Z                     float32
FLUX_IVAR_G                float32
FLUX_IVAR_R                float32
FLUX_IVAR_Z                float32
MASKBITS                   int16
REF_ID                     int64
REF_CAT                    char[2]
GAIA_PHOT_G_MEAN_MAG       float32
GAIA_PHOT_BP_MEAN_MAG      float32
GAIA_PHOT_RP_MEAN_MAG      float32
PARALLAX                   float32
BRICKNAME                  char[8]
EBV                        float32
FLUX_W1                    float32
FLUX_W2                    float32
FLUX_IVAR_W1               float32
FLUX_IVAR_W2               float32
FIBERFLUX_G                float32
FIBERFLUX_R                float32
FIBERFLUX_Z                float32
FIBERTOTFLUX_G             float32
FIBERTOTFLUX_R             float32
FIBERTOTFLUX_Z             float32
SERSIC                     float32
SHAPE_R                    float32
SHAPE_E1                   float32
SHAPE_E2                   float32
PHOTSYS                    char[1]
PRIORITY_INIT              int64
NUMOBS_INIT                int64
DESI_TARGET                int64
BGS_TARGET                 int64
MWS_TARGET                 int64
SCND_TARGET                int64
PLATE_RA                   float64
PLATE_DEC                  float64
COADD_NUMEXP               int16
COADD_EXPTIME              float32
COADD_NUMNIGHT             int16
COADD_NUMTILE              int16
MEAN_DELTA_X               float32
RMS_DELTA_X                float32
MEAN_DELTA_Y               float32
RMS_DELTA_Y                float32
MEAN_FIBER_RA              float64
STD_FIBER_RA               float32
MEAN_FIBER_DEC             float64
STD_FIBER_DEC              float32
MEAN_PSF_TO_FIBER_SPECFLUX float32
========================== ======= ===== ===========

HDU3
----

EXTNAME = EXP_FIBERMAP

*Summarize the contents of this HDU.*

Required Header Keywords
~~~~~~~~~~~~~~~~~~~~~~~~

====== ============= ==== =====================
KEY    Example Value Type Comment
====== ============= ==== =====================
NAXIS1 162           int  length of dimension 1
NAXIS2 415           int  length of dimension 2
====== ============= ==== =====================

Required Data Table Columns
~~~~~~~~~~~~~~~~~~~~~~~~~~~

===================== ======= ===== ===========
Name                  Type    Units Description
===================== ======= ===== ===========
TARGETID              int64
PRIORITY              int32
SUBPRIORITY           float64
NIGHT                 int32
EXPID                 int32
MJD                   float64
TILEID                int32
EXPTIME               float64
PETAL_LOC             int16
DEVICE_LOC            int32
LOCATION              int64
FIBER                 int32
FIBERSTATUS           int32
FIBERASSIGN_X         float32
FIBERASSIGN_Y         float32
LAMBDA_REF            float32
PLATE_RA              float64
PLATE_DEC             float64
NUM_ITER              int64
FIBER_X               float64
FIBER_Y               float64
DELTA_X               float64
DELTA_Y               float64
FIBER_RA              float64
FIBER_DEC             float64
PSF_TO_FIBER_SPECFLUX float64
===================== ======= ===== ===========

HDU4
----

EXTNAME = TSNR2

*Summarize the contents of this HDU.*

Required Header Keywords
~~~~~~~~~~~~~~~~~~~~~~~~

====== ============= ==== =====================
KEY    Example Value Type Comment
====== ============= ==== =====================
NAXIS1 136           int  length of dimension 1
NAXIS2 415           int  length of dimension 2
====== ============= ==== =====================

Required Data Table Columns
~~~~~~~~~~~~~~~~~~~~~~~~~~~

================= ======= ===== ===========
Name              Type    Units Description
================= ======= ===== ===========
TARGETID          int64
TSNR2_GPBDARK_B   float32
TSNR2_ELG_B       float32
TSNR2_GPBBRIGHT_B float32
TSNR2_LYA_B       float32
TSNR2_BGS_B       float32
TSNR2_GPBBACKUP_B float32
TSNR2_QSO_B       float32
TSNR2_LRG_B       float32
TSNR2_GPBDARK_R   float32
TSNR2_ELG_R       float32
TSNR2_GPBBRIGHT_R float32
TSNR2_LYA_R       float32
TSNR2_BGS_R       float32
TSNR2_GPBBACKUP_R float32
TSNR2_QSO_R       float32
TSNR2_LRG_R       float32
TSNR2_GPBDARK_Z   float32
TSNR2_ELG_Z       float32
TSNR2_GPBBRIGHT_Z float32
TSNR2_LYA_Z       float32
TSNR2_BGS_Z       float32
TSNR2_GPBBACKUP_Z float32
TSNR2_QSO_Z       float32
TSNR2_LRG_Z       float32
TSNR2_GPBDARK     float32
TSNR2_ELG         float32
TSNR2_GPBBRIGHT   float32
TSNR2_LYA         float32
TSNR2_BGS         float32
TSNR2_GPBBACKUP   float32
TSNR2_QSO         float32
TSNR2_LRG         float32
================= ======= ===== ===========


Notes and Examples
==================

*Add notes and examples here.  You can also create links to example files.*
