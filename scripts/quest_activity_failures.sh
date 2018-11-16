reset
echo ">> Printing failed activities:"
ls -t | grep ".out" | head -n 1 | xargs -I{} cat {} | grep -E "questId=$1(.*)portId=(.*)status=FAILED" | grep -o -E "activityId=[a-z0-9]{8}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{12}" | uniq
echo ">> Printing quest details:"
curl "https://manila1.cpaas.awsiondev.infor.com:18010/coleman/api/quest/$1?render=true" --insecure

