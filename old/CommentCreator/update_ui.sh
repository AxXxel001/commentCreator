cp ../CommentCreator/mainwindow.ui res/mainwindow.ui
pyuic4 res/mainwindow.ui > res/py_mainwindow.py
cp ../CommentCreator/commentcreator.ui res/commentcreator.ui
pyuic4 res/commentcreator.ui > res/py_commentcreator.py
echo "Done"
