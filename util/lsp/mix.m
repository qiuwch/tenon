baseFolder = '/q/cache/lsp_2d_3d/render_output/1028/%s/imgs/im%04d.png';
mixFolder = '/q/cache/lsp_2d_3d/render_output/1028/mix/im%04d.png';
folder = {'201510280116','201510280221','201510280331','201510280433','201510280535','201510280605'};

for i = 1:2000
	m = randi(length(folder));
	file = sprintf(baseFolder, folder{m}, i);
	disp(file);

	if ~exist(file, 'file')
		fprintf('Error: file %s not exist', file);
		file = sprintf(baseFolder, folder{1}, i); % TODO: Check why some files not rendered
	end


	im = imread(file);
	imwrite(im, sprintf(mixFolder, i));
end
