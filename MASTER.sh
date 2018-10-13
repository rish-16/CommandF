for filename in 'icon.png' 'js/' 'manifest.json' 'templates/' 'timestamps.txt' 'ytDownloadServer.py' 'ytDownloadServer.pyc'
do
  echo $filename
  git add $filename
  git commit -m 'Adding Darkflow integration'
  git push --force --verbose
done;