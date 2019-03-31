#!/bin/bash

echo "START OUR Expermients!"

echo "MAF-LSA MINIST"

# echo "Train"
# python train.py --autoencoder LSA --estimator MAF --dataset mnist --batch_size 1000 --lr 0.001 --num_blocks 5  --epochs 1000 --combine_density True 

# echo "Train"
# python train.py --autoencoder LSA --estimator MAF --dataset mnist --batch_size 1000 --lr 0.001 --num_blocks 5  --epochs 1000 --combine_density False

echo "Test score_normed combine_density"
# novel from 0.1 to 0.5
for i in  0.1 0.2 0.3 0.4 0.5
	do 
		echo "Test on novel_ratio=$i" 
		python test.py --autoencoder LSA --estimator MAF --dataset mnist --num_blocks 5 --combine_density True --score_normed True  --novel_ratio $i
	done


echo "Test not score_normed, combine_density"
for i in  0.1 0.2 0.3 0.4 0.5
	do 
		echo "Test on novel_ratio=$i" 
		python test.py --autoencoder LSA --estimator MAF --dataset mnist --num_blocks 5 --combine_density True --score_normed False  --novel_ratio $i
	done


echo "Test score_normed, not combine_density"
for i in  0.1 0.2 0.3 0.4 0.5
	do 
		echo "Test on novel_ratio=$i" 
		python test.py --autoencoder LSA --estimator MAF --dataset mnist --num_blocks 5 --combine_density False --score_normed True  --novel_ratio $i
	done



echo "Test not score_normed, not combine_density"
for i in  0.1 0.2 0.3 0.4 0.5
	do 
		echo "Test on novel_ratio=$i" 
		python test.py --autoencoder LSA --estimator MAF --dataset mnist --num_blocks 5 --combine_density False --score_normed False  --novel_ratio $i
	done



echo "MAF-LSA MINIST"

echo "Train"
python train.py --autoencoder LSA --estimator SOS --dataset mnist --batch_size 1000 --lr 0.001 --num_blocks 5  --epochs 1000 --combine_density False

echo "Test score_normed combine_density"
# novel from 0.1 to 0.5
for i in  0.1 0.2 0.3 0.4 0.5
	do 
		echo "Test on novel_ratio=$i" 
		python test.py --autoencoder LSA --estimator SOS --dataset mnist --num_blocks 5 --combine_density True --score_normed True  --novel_ratio $i
	done


echo "Test not score_normed, combine_density"
for i in  0.1 0.2 0.3 0.4 0.5
	do 
		echo "Test on novel_ratio=$i" 
		python test.py --autoencoder LSA --estimator SOS --dataset mnist --num_blocks 5 --combine_density True --score_normed False  --novel_ratio $i
	done


echo "Test score_normed, not combine_density"
for i in  0.1 0.2 0.3 0.4 0.5
	do 
		echo "Test on novel_ratio=$i" 
		python test.py --autoencoder LSA --estimator SOS --dataset mnist --num_blocks 5 --combine_density False --score_normed True  --novel_ratio $i
	done



echo "Test not score_normed, not combine_density"
for i in  0.1 0.2 0.3 0.4 0.5
	do 
		echo "Test on novel_ratio=$i" 
		python test.py --autoencoder LSA --estimator SOS --dataset mnist --num_blocks 5 --combine_density False --score_normed False  --novel_ratio $i
	done
