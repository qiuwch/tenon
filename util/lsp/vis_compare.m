% tmpPath = '/q/tmp/compare/im%04d.png';
% path1 = '/q/data/l23/imgs/im%04d.png';
% path2 = '/q/cache/lsp_2d_3d/render_output/201510271958/crop/imgs/im%04d.png';
% tmpPath = '/q/cache/xianjie/testing/compare_l11_lsp_fashion/im%04d.png';
% path1 = '/q/cache/xianjie/testing/mlsp_fashion/fig/im%04d.png';
% path2 = '/q/cache/xianjie/testing/ml11_fashion/fig/im%04d.png';
tmpPath = '/q/tmp/compare_real_synth/im%04d.png';
paths = {'/q/data/l23_v1/imgs/im%04d.png', '/q/data/l23_v2/imgs/im%04d.png', '/q/data/lsp/lsp_dataset/images/im%04d.jpg'};
ncol = length(paths);

for i = 1:1000
    ims = repmat(struct('im', [], 'w', [], 'h', []), ncol, 1);
    
    maxh = 0; totalw = 0;
    for j = 1:ncol
        im = imread(sprintf(paths{j}, i));
        [h, w, c] = size(im);
        maxh = max(maxh, h);
        totalw = totalw + w;
        
        ims(j).im = im;
        ims(j).w = w;
        ims(j).h = h;
    end
    
    im = zeros(maxh, totalw, c, 'uint8');
    offx = 0;
    for j = 1:ncol
        h = ims(j).h; w = ims(j).w;
        im(1:h, offx+1:offx+w,:) = ims(j).im;
        offx = offx + w;
    end
    imwrite(im, sprintf(tmpPath, i));
    if mod(i, 10) == 0
        disp(i);
    end
end