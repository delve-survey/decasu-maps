-- Query for selecting coadd tile geometries associated with a proctag
--
-- Run with:
-- easyaccess -s decade -l coadd_tiles_and_geom.sql
--
select c.TILENAME, CAST(c.BAND as VARCHAR(1)) as BAND, c.PFW_ATTEMPT_ID, 
       CAST(g.CROSSRA0 as VARCHAR(1)) as CROSSRA0, 
       g.RA_CENT, g.DEC_CENT, 
       g.URAMIN, g.URAMAX, g.UDECMIN, g.UDECMAX
from coaddtile_geom g, coadd c, proctag t
where c.pfw_attempt_id = t.pfw_attempt_id
and c.tilename = g.tilename
and t.tag = 'DR3_1_1'
and c.filetype = 'coadd'
order by c.tilename, c.band;
> dr3_1_1_coadd_tiles_and_geom.fits
