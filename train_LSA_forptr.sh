#Train LSA--doing
python train_temp.py  --autoencoder LSA --epochs 1000 --dataset mnist  --lr 0.0001 --batch_size 256 --code_length 64

python test_temp.py  --autoencoder LSA --epochs 1000 --dataset mnist --batch_size 256 --code_length 64

python train_temp.py  --autoencoder LSA --epochs 1000 --dataset cifar10  --lr 0.001 --batch_size 256 --code_length 64 

python test_temp.py  --autoencoder LSA  --epochs 1000 --dataset cifar10 --batch_size 256 --code_length 64
