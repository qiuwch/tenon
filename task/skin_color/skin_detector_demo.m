load('rgbskin.mat');

im = imread(imagepath);
tic
im32 = uint32(im);
skinmap = rgbskin(sub2ind([256,256,256], im32(:,:,1)+1, im32(:,:,2)+1, im32(:,:,3)+1));
toc
imshow(double(skinmap)/65536);
