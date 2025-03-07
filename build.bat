docker build -t file-uploader . --no-cache
docker tag file-uploader:latest rahulrrao/file-uploader:latest
docker push rahulrrao/file-uploader:latest