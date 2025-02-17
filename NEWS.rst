PyPop Release History
=====================

.. _news-start:

Notes towards next release
--------------------------
(unreleased)

New features
^^^^^^^^^^^^^^
* Updated to Python 3
* Implement new assymetric LD (ALD) measure
* New wrapper module ``Haplostats``. This wraps a portion of the
  ``haplo.stats`` R package ``haplo-stats`` for haplotype
  estimation. [Implementation in alpha-phase].
* ``popmeta``: now accepts the ``-o``/``--outputdir`` option for saving
  generated files.
* ``pypop``: renamed ``--generate-tsv`` to ``--enable-tsv``


Release Notes for PyPop 0.7.0
-----------------------------
(2008-09-09)

New features
^^^^^^^^^^^^
* ``makeNewPopFile`` option has been changed.  This option allows user to 
  generate intermediate output of filtered files. Now option should
  be of the format: ``type:order`` where ``type`` is one of
  ``separate-loci`` or ``all-loci`` so that the user can specify whether
  a separate file should be generated for each locus
  (``separate-loci``) or a single file with all loci (``all-loci``).
  ``order`` should be the order in the filtering chain where the
  matrix is generated, there is no default, for example, for
  generating files after the first filter operation use ``1``.
* New command-line option ``--generate-tsv``, will generate the ``.dat`` 
  tab-separated values (TSV) files on the the generated -out.xml
  files (aka "popmeta") directly from pypop without needing to run
  additional script.  Now output from pypop can be directly read
  into spreadsheet.
* New feature: add individual genotype tests to Hardy-Weinberg module 
  (gthwe), now computes statistics based on individual genotypes in
  the HWP table. The ``[HardyWeinbergGuoThompson]`` or 
  ``[HardyWeinbergGuoThompsonMonteCarlo]`` options must be enabled in the 
  configuration ".ini" file in order for these tests to be carried out.
* Major improvements to custom and random binning filters (Owen Solberg).
* New feature: generate homozygosity values using the Ewens-Watterson test for
  all pairwise loci, or all sites within a gene for sequence data
  (``[homozygosityEWSlatkinExactPairwise]`` in .ini file).  Note: this
  really only works for sequence data where the phase for sites
  within an allele are known.
* Haplotype and LD estimation module ``emhaplofreq`` improvements
  
  * improved memory usage and speed for emhaplofreq module.
  * maximum sample size for emhaplofreq module increased from 1023 to
    5000 individuals.
  * maximum length of allele names increased to 20

Bug fixes
^^^^^^^^^
* Support Python 2.4 on GCC 4.0 platforms.
* Add missing initialisation for non-sequence data when processing 
  haplotypes.  Thanks to Jill Hollenbach for the report.
* Fix memory leak in xslt translation.
* Various fixes relating to parsing XML output.
* Fixed an incorrect parameter name.
* Handle some missing sections in .ini better. Thanks to 
  Owen Solberg for report.
* Various build and installation fixes (SWIG, compilation flags)
* Make name of source package be lowercase "pypop".
* Change data directory: /usr/share/pypop/ to /usr/share/PyPop/
* Print out warning when maximum length of allele exceeded, rather than
  crashing.  Thanks to Steve Mack for report.

Other issues
^^^^^^^^^^^^
* Sequence filter
  
  * In the Sequence filter, add special case for Anthony Nolan HLA data:
    mark null alleles ending in "N" (e.g. HLA-B*5127N) as "missing
    data" (``****``).
  * Also in Sequence, keep track of unsequenced sites separately   
    (via unsequencedSites variable) from "untyped" (aka "missing
    data"). Treat unsequencedSite as a unique allele to make sure that
    those sites don't get treated as having a consensus sequence if
    only one of the sequences in the the set of matches is typed.
  * If no matching sequence is found in the MSF files, then return a
    sequence of * symbols (ie, will be treated as truly missing data,
    not untyped alleles.
  * Add another special case for HLA data: test for 7 digits in allele names
    (e.g. if 2402101 is not found insert a zero after the first 4
    digits to form 24020101, and check for that).  This is to cope
    with yet-another HLA nomenclature change.
* Change semantics of batchsize, make "0" (default) process files separately
  if only R dat files is enabled.  If batchsize not set explicitly
  (and therefore 0) set batchsize to ``1`` is PHYLIP mode is enabled.

Release Notes for PyPop 0.6.0
-----------------------------
(2005-04-13)

New features
^^^^^^^^^^^^
* Allow for odd allele counts when processing an allele count data 
  (i.e "semi"-typing).  When PyPop is dealing with data that is
  originally genotyped, the current default is preserved i.e.  we
  dis-allow individuals that are typed at only allele, and set
  allowSemiTyped to false.
* New command-line option ``-f`` (long version ``--filelist``) which
  accepts a file containing a list of files (one per line) to
  process (note that this is mutually exclusive with supplying
  INPUTFILEs, and will abort with an error message if you supply
  both simultaneously).
* In batch version, handle multiple INPUTFILEs supplied as command-line
  arguments and support Unix shell-globbing syntax (e.g. ``pypop.py
  -c config.ini *.pop``). (NOTE: This is supported *only* in
  batch version, not in the interactive version, which expects one
  and only one file supplied by user.
* Allele count files can now be filtered through the filter apparatus
  (particularly the Sequence and AnthonyNolan) in the same was as
  genotype files transparently.  [This has been enabled via a code
  refactor that treats allele count files as pseudo-genotype files
  for the purpose of filtering].  This change also resulted in the
  removal of the obsolete lookup-table-based homozygosity test.
* Add ``--disable-ihwg`` option to popmeta script to disable hardcoded 
  generation of the IHWG header output, and use the output as
  defined in the header in the original .pop input text file.  This
  is disabled by default to preserve backwards compatibility.
* Add ``--batchsize`` (``-b`` short version) option  for popmeta.  Does the
  processing in "batches".  If set and greater than one, list of XML
  files is split into batchsize group.  For example, if there are 20
  XML files and option is via using ("-b 2" or "--batchsize=2") then
  the files will be processed in two batches, each consisting of 10
  files.  If the number does not divide evenly, the last list will
  contain all the "left-over" files.  This option is particularly
  useful with large XML files that may not fit in memory all at
  once.  Note this option is mutually exclusive with the
  ``--enable-PHYLIP`` option because the PHYLIP output needs to
  calculate allele frequencies across all populations before
  generating files.
* New .ini file option: ``[HardyWeinbergGuoThompsonMonteCarlo]``: add a plain
  Monte-Carlo (randomization, without the Markov chain test) test
  for the HardyWeinberg "exact test".  Add code for Guo & Thompson
  test to distribution (now under GNU GPL).

Bug fixes
^^^^^^^^^
* HardyWeinbergGuoThompson overall p-value test was numerically unstable 
  because it attempted to check for equality in greater than or
  equal to constructs ("<=") which is not reliable in C.  Replaced
  this with a GNU Scientific Library (GSL) function gsl_fcmp() which
  compares floats to within an EPSILON (defaults to 1e-6).
* Allow ``HardyWeinbergGuoThompson` test to be run if at least two alleles
  present (test was originally failing with a ``too-few-alleles``
  message if there were not at least 3 alleles).  Thanks to Kristie
  Mather for the report.
* Checks to see if a locus is monomorphic, if it is, it generates an 
  allele summary report, but skips the rest of the single locus
  analyses which do not make sense for monomorphic locus.  Thanks to
  Steve Mack and Owen Solberg for the bug report(s).
* Now builds against recent versions of SWIG (no longer stuck at version 
  1.3.9), should be compatible with versions of SWIG > 1.3.10.
  (Tested against SWIG 1.3.21).
* Homozygosity module: Prevent math errors by in Slatkin's exact test by 
  forcing the homozygosity to be positive (only a problem for rare
  cases, when the result is so close to zero that the floating point
  algorithms cause a negative result.)

Release Notes for PyPop 0.5.2 (public beta) 
-------------------------------------------
(2004-03-09)

Bug fixes
^^^^^^^^^
* Add missing RandomBinning.py file to source distribution
  Thanks to Hazael Maldonado Torres for the bug report.
* Fixed line endings for .bat scripts for Win32 so they work under 
  Windows 98 thanks to Wendy Hartogensis for the bug report.

Release Notes for PyPop 0.5.1 (public beta) 
-------------------------------------------
(2004-02-26)

Changes
^^^^^^^
* New parameter ``numInitCond``, number of initial conditions by the
  haplotype estimation and LD algorithm used before performing
  permutations. Defaults to 50.
* Remove some LOG messages/diagnostics that were erroneously implying
  an error to the user (if nothing is wrong, don't say anything).  Add
  some more useful messages for what is being done in haplo/LD 
  estimation step.
* Add popmeta.py to the distribution: this is undocumented and unsupported 
  as yet, it is at alpha stage only, use at your own risk!

Bug fixes
^^^^^^^^^
* Remember to output plaintext version of LD for specified loci.

Release Notes for PyPop 0.5 (public beta)
-----------------------------------------
(2003-12-31)

Changes
^^^^^^^
* All Linux wrapper scripts no longer have .sh file suffixes for 
  consistency with DOS (all DOS bat files can be executed without
  specifying the .bat extension).

Bug fixes
^^^^^^^^^
* Add wrapper scripts for interactive and batch mode for 
  both DOS and Linux so that correct shared libraries are called.
* Pause and wait for user to press a key at end of DOS .bat file
  so that output can be viewed before window close.
* Set PYTHONHOME in wrapper scripts to prevent messages about 
  missing <prefix> being displayed.

Release Notes for PyPop 0.4.3beta
---------------------------------
Bug fixes
^^^^^^^^^
* Fixed bug in processing of ``popname`` field. 
  Thanks to Richard Single for the report.
