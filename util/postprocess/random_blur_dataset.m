function random_blur_dataset(folder)
    % Remove the trailing /, because the string operation assumes no /
    if folder(end) == '/'
        folder = folder(1:end-1);
    end
    % Iterate over all the images of the dataset and apply gaussian blur
    % and motion blur randomly.
    if ~exist([folder '/imgs'], 'dir')
        error('This is not a valid data folder');
    end
    
    files = dir(sprintf('%s/imgs/*.png', folder));
    N = length(files);
    if N ~= 2000
        warning('The number of images is %d, data might not be complete', N);
    end
    
    outfolder = [folder '_blur'];
    if ~exist(outfolder, 'dir')
        mkdir(outfolder);
        mkdir([outfolder '/imgs']);
    end
    diary(sprintf([outfolder '/blurinfo.txt']));
    % Output the log of post process to the folder
    
    for i = 1:N
        filename = sprintf('%s/imgs/%s', folder, files(i).name);
        im = imread(filename);
        vec = [rand() * 3, rand() * 3];
        blurim = motionblur(im, vec);
        outfile = sprintf('%s/imgs/%s', outfolder, files(i).name);
        imwrite(blurim, outfile);
        fprintf('Post process %s, motion vector %f %f\n', filename, vec(1), vec(2));
    end
    
    fprintf('Done, please copy other related files manually.\n');
    diary('off');
end