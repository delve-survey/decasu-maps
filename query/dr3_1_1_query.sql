-- Download with:
-- easyaccess -s delve -l dr3_1_1_query.sql 

select i.expnum, i.ccdnum, i.tilename, e.mjd_obs,
       i.skyvara,i.skyvarb,
       cast(i.band as VARCHAR(1)) as band,
       i.skysigma,i.fwhm,i.exptime,i.airmass,i.skybrite,
       i.rac1,i.rac2 ,i.rac3,i.rac4,
       i.decc1, i.decc2,i.decc3,i.decc4,
       i.crpix1,i.crpix2,
       i.crval1,i.crval2,i.cunit1,i.cunit2,i.cd1_1,i.cd1_2,
       i.cd2_1,i.cd2_2,i.pv1_0,i.pv1_1,i.pv1_2,i.pv1_3,
       i.pv1_4,i.pv1_5,i.pv1_6,i.pv1_7,i.pv1_8,i.pv1_9,i.pv1_10,
       i.pv2_0,i.pv2_1,i.pv2_2,i.pv2_3,
       i.pv2_4,i.pv2_5,i.pv2_6,i.pv2_7,i.pv2_8,i.pv2_9,i.pv2_10,
       i.pfw_attempt_id,
       2048 as naxis1, 4096 as naxis2,
       -- Zeropoints
       0 as mag_zero
from image i, proctag p, exposure e
where p.tag in ('DR3_1_1')
and i.pfw_attempt_id=p.pfw_attempt_id
--and i.filetype='fullcat'
and i.expnum=e.expnum
ORDER BY expnum

--remove limit to fully execute
--FETCH FIRST 50 ROWS ONLY
;
 > dr3_1_1_query.csv
