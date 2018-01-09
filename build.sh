rm -rf build
rm -rf *.so
rm -rf *.c
python setup.py build_ext --inplace
