% Read joint location from the color coded image.
% im = imread('/q/cache/render_output/8.31_v2/crop/skel/0000.png');
im = im2double(imread('/q/cache/render_output/8.31_v2/skel/0000.png'));
imshow(im);

color = [1 0 0];
colorPlate = zeros(size(im));
for j = 1:3
    colorPlate(:,:,j) = color(j);
end

diff = sqrt(sum((colorPlate - im).^2, 3));

cq = imfindcircles(im, [1 10]);
disp(size(cq, 1));
hold on;
plot(cq(:,1), cq(:,2), '*');