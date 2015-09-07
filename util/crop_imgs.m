function crop_imgs()
    % Crop the image, to make it suitable for LSP format
    clear all;
    origDir = '/q/cache/render_output/9.7_v1/';
    disp(origDir);

    num = 40;

    for i = 0:(num-1)
        % Get mask
        depth_fname = sprintf([origDir 'depth/%04d.png'], i);
        depth = imread(depth_fname);
        fg = depth(:,:,1) > 0;

        % compute the bounding box of fg
        imSize = size(depth(:,:,1));
        [Y, X] = ind2sub(imSize, find(fg));
        fgBBmask = false(imSize);
        fgBBmask(min(Y):max(Y), min(X):max(X)) = 1;
        bb = [min(Y), max(Y), min(X), max(X)];

    %     fgIdx = fg;
        fgIdx = fgBBmask;

        % for type = {'imgs', 'depth', 'skel'}
        for type = {'imgs'}
            type = type{1};
            imfname = sprintf([origDir type '/%04d.png'], i);
            im = imread(imfname);
            im = im2double(im);
%             crop = do_crop(im, fgIdx);
            crop = bb_crop(im, bb);
            crop_imfname = sprintf([origDir 'crop/' type '/%04d.png'], i);
            imwrite(crop, crop_imfname);
        end
    end
end

function crop = bb_crop(im, bb)
    h = bb(2) - bb(1); w = bb(4) - bb(3);
    h = max(h, w); w = max(h, w);
    imh = size(im, 1); imw = size(im, 2);
    
    ratio = 0.1;
    t = max(uint32(bb(1) - ratio * h), 1);
    b = min(uint32(bb(2) + ratio * h), imh);
    l = max(uint32(bb(3) - ratio * w), 1);
    r = min(uint32(bb(4) + ratio * w), imw);
    crop = im(t:b, l:r, :);
    sz = size(crop(:,:,1));
    if sz(1) > sz(2) % height > width
        crop = imresize(crop, 150.0 / sz(1)); % no interporlation for joint labeling
    else
        crop = imresize(crop, 150.0 / sz(2));
    end
end

function crop = do_crop(im, fgIdx)
    crop = zeros(size(im));
    for ci = 1:3 % channel index
        c = im(:,:,ci);
        c(~fgIdx) = 0;
        crop(:,:,ci) = c;
    end
end