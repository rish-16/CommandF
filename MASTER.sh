for filename in ./darkflow/*
do
  echo $filename
  git add $filename
  git commit -m 'Adding Darkflow integration'
  git push --force --verbose
done;

for filename in 'LICENSE' 'MASTER.sh' 'build/' 'cfg/' 'flow' 'labels.txt' 'proc.py' 'setup.py' 'test/'
do
  echo $filename
  git add $filename
  git commit -m 'Adding Darkflow integration'
  git push --force --verbose
done;