set -e

DATE="$(date +%Y-%m-%d --date="-$1 days")"
echo $DATE

[ -f "../data/all_data_${DATE}.zip" ] || echo "Check faunalytics twitter for date ${DATE}" | /usr/bin/mail -s "OH GOD! something went wrong..." mmatt246@gmail.com
