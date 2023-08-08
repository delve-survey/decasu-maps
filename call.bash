
declare -a StringArray=("g"
			"r"
			"i"
			"z")
for val in ${StringArray[@]}; do
	echo starting $val
	python code/decasu_mapper.py -c DR_311_config.yaml -g ./data/coadd_tile_and_geom.fits -i ./data/dr3_1_1_query.fits -o ./hsp -b $val -n 12 > logs/dr3_1_1_$val.log 2>&1
done
