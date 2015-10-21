ddir = '/q/data/human_parsing/train_groundtruth/';

[im, map] = imread([ddir '3_2_00000169ucm2_seg_ped.png']);
imshow(im);

cim = zeros(size(im, 1), size(im, 2), 3);
for c = 1:3
    cmap = map(:,c);
    cim(:,:,c) = cmap(im+1);
end
imshow(cim);


vals = unique(im(:));
labels = {'bg', 'face', 'hair', 'cloth', 'pant', 'l.arm', 'r.arm', 'l.leg', 'r.leg', 'l.foot', 'r.foot'};

if 0
for i = 1:numel(vals);
    v = vals(i);
    subplot(121); imshow(cim);
    subplot(122);
    imshow(im == v); 
    title(labels{i});
    pause;
end
end
% map(vals+1, :);

for i = 1:numel(vals)
   fprintf('%s, %f, %f, %f\n', labels{i}, map(vals(i)+1, 1), map(vals(i)+1, 2), map(vals(i)+1, 3));
end