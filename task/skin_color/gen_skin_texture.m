skinfolder = '/q/run/tenon/scenes/textures/randSkinColor';
A = load('rgbskin.mat');

% A.rbgskin is a 256x256x256 color space.
% range from 1 to 65536

N = 2000; % Pick the top N skin color

% let me get the top 1000 skin color
[val, idx] = sort(A.rgbskin(:), 'descend'); % sort from high to low
[r, g, b] = ind2sub([256, 256, 256], idx);


for i = 1:N
    texture = zeros(100, 100, 'uint8');
    texture(:,:,1) = r(i);
    texture(:,:,2) = g(i);
    texture(:,:,3) = b(i);
%     imshow(texture);
    fprintf('Value of this skin color, %d\n', val(i));
    filename = fullfile(skinfolder, sprintf('%d.png', i));
    imwrite(texture, filename);
end