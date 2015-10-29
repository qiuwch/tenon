% tmpPath = '/q/tmp/compare/im%04d.png';
% path1 = '/q/data/l23/imgs/im%04d.png';
% path2 = '/q/cache/lsp_2d_3d/render_output/201510271958/crop/imgs/im%04d.png';
tmpPath = '/q/cache/xianjie/testing/compare_l11_lsp_fashion/im%04d.png';
path1 = '/q/cache/xianjie/testing/mlsp_fashion/fig/im%04d.png';
path2 = '/q/cache/xianjie/testing/ml11_fashion/fig/im%04d.png';

for i = 1:1000
    im1 = imread(sprintf(path1, i));
    im2 = imread(sprintf(path2, i));
    [h1, w1, c] = size(im1);
    [h2, w2, c] = size(im2);
    im = zeros(max(h1, h2), w1 + w2, c, 'uint8');
    im(1:h1, 1:w1, :) = im1;
    im(1:h2, w1+1:w1+w2, :) = im2;
    imwrite(im, sprintf(tmpPath, i));
    if mod(i, 10) == 0
        disp(i);
    end
end