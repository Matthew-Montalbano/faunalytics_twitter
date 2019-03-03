set -e

DATE="$(date +%Y-%m-%d --date="-$1 days")"
echo $DATE

mkdir "../data/all_data_${DATE}"
mv ../data/tweets*${DATE}*.pkl ../data/all_data_${DATE}

zip -r ../data/all_data_${DATE}.zip ../data/all_data_${DATE}
rm -R data/all_data_${DATE}
