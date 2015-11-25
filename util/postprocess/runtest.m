% TODO: Consider to rewrite post process with python, so that I can fit the pipeline together
% Here is just a quick hack
% Run unit test for functions defined here
close all;
disp('Run motion blur test'); figure;
im = imread('/q/data/l23_v1/imgs/im0001.png');
subplot(121); imshow(im); title('original image');
blurim = motionblur(im, [3 3]);
subplot(122); imshow(blurim);  title('motion blur');
% subplot(122); imshow(zeros(100));

disp('Run gaussian blur test'); figure; title('gaussian blur');
im = imread('/q/data/l23_v1/imgs/im0001.png');
subplot(121); imshow(im);
blurim = gaussblur(im, [5, 5], 1);
subplot(122); imshow(blurim);
