echo "Stopping typesense server if its running"
docker stop $(docker ps | awk '/typesense/ {print $1}');
echo "Stopped typesense server if its running"

echo "Remove old typesense container if it exists"
docker rm $(docker container ls -a --filter status=exited --filter status=created | awk '/typesense/ {print $1}');
echo "Removed old typesense container if it exists"

echo "Deleting local data folder"
rm -rf /tmp/typesense/
echo "Deleted local data folder"

echo "Create data folder if it does not exists"
mkdir -p /tmp/typesense/
echo "Deleted local data folder"

echo "Starting local typesense server ....."
docker run -i --name typesense -p 8108:8108 -v/tmp/$(openssl rand -hex 12)/:/data typesense/typesense:0.19.0 --data-dir /data --api-key=duIpsVTnbWkmsVokzxhj --listen-port 8108 --enable-cors &

sleep 20s;
echo "Started local typesense server !!!!!"

echo "Uploading data to local typesense server"
cd cli/typesense/;
python3 loadIndex.py local all;
echo "Uploaded data to local typesense server"
sleep 5s;

echo "Copy files from docker container to /tmp/data"
docker cp $(docker ps | awk '/typesense/ {print $1}'):/data/state /tmp/typesense
echo "Copied files from docker container to /tmp/data"

echo "Removing snapshot folder"
rm -rf /tmp/typesense/state/snapshot
echo "Removed snapshot folder"

echo "Stoping local typesense server"
docker stop $(docker ps | awk '/typesense/ {print $1}');
echo "Stopped local typesense server"

echo "Remove typesense container"
docker rm $(docker container ls -a --filter status=exited --filter status=created | awk '/typesense/ {print $1}');
echo "Removed typesense container"

ls /tmp/typesense