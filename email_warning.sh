set -e

DATE="$(date +%Y-%m-%d --date="-$1 days")"
echo $DATE

[ -f "../data/all_data_${DATE}.zip" ] || mail -s "OH GOD! something went wrong..." paulfornia@gmail.com < /dev/null
