function crop_imgs()
    % Crop the image, to make it suitable for LSP format
    origDir = '/q/cache/render_output/';
    cropDir = [origDir 'crop/'];
    anno = csvread([origDir 'joint-PC-MATLAB.csv']);
    joints = zeros(2, size(anno,2)/2, size(anno,1));

    for fileid = 1:size(anno, 1)
        % Get annotation
        X = anno(fileid, 1:2:end);
        Y = anno(fileid, 2:2:end);

        % Get mask
        depth_fname = sprintf([origDir 'depth/im%04d.png'], fileid);
        depth = imread(depth_fname);

        % for type = {'imgs', 'depth', 'skel'}
        for type = {'imgs'}
            type = type{1};
            imfname = sprintf([origDir type '/im%04d.png'], fileid);
            im = imread(imfname);
            im = im2double(im);
            
            [crop, U, V] = crop_img(im, depth, X, Y);
            % debug
            % imshow(im); hold on; plot(X, Y, '*'); pause;
            % imshow(crop); hold on; plot(U, V, '*'); pause;
            
            % Save cropped image
            crop_imfname = sprintf([cropDir type '/im%04d.png'], fileid);
            imwrite(crop, crop_imfname);

            % Save annotation
            joints(1, :, fileid) = U;
            joints(2, :, fileid) = V;
        end
    end
    save([cropDir 'joints.mat'], 'joints');
end

