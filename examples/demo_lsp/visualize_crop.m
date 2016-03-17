
vislib = '~/Dropbox/workspace/graphics_for_vision/visualize/code';
addpath(vislib);
base_dir = '~/nosync/circular_demo/';

%% Visualize full data
csv_file = [base_dir 'full/joints/0001_az0.csv'];
plot_blender(csv_file);

%% Visualize cropped data

for i = 1:10
im_filename = [base_dir sprintf('crop/imgs/%04d_az0.png', i)];
im = imread(im_filename);

imshow(im); hold on;
joint_file = [base_dir sprintf('crop/joints/%04d_az0.csv', i)];
fprintf('Read joint information from %s\n', joint_file);
joints = csvread(joint_file);

plot_lsp(joints', true);
pause;
clf;
end