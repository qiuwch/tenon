i = 1;

baseDir = '/q/cache/fixFactorPose/10.02_v1/';

% Load full image
im = imread([baseDir 'imgs/' sprintf('im%04d.png', i)]);
subplot(121); imshow(im); hold on;

% Load joint location
[X, Y] = read_joint_info([baseDir 'joint/' sprintf('im%04d.csv', i)]);
plot(X, Y, '*');

% Load cropped image
cropIm = imread([baseDir 'crop/imgs/' sprintf('im%04d.png', i)]);
subplot(122); imshow(cropIm); hold on;

% Load all annotation
A = load([baseDir 'crop/joints-PC.mat']);
joints = A.joints;
plot(joints(1,:,i), joints(2,:,i), '*');
