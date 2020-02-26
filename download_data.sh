declare -a days=("01" "02" "03" "04" "05" "06" "07" "08" "09" "10" "11" "12" "13" "14" "15" "16" "17" "18" "19" "20" "21" "22" "23" "24" "25" "26" "27" "28" "29" "30" "31")
for day in "${days[@]}"
do
    aws s3 cp s3://faunalytics-twitter/raw_data_pkl/all_data_2019-12-${day}.zip C:/Users/mmatt/Desktop/all_data
done