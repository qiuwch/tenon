baseFile = '/q/cache/lsp_2d_3d/render_output/%s/%s/im%04d.%s';
mixFolder = '/q/tmp/mixfolder/%s/';
mixFile = [mixFolder 'im%04d.%s'];

blend = {'m_c_1'};
types = {'imgs', 'depth', 'joint'};
exts = {'png', 'png', 'csv'};
for type = types
    mkdir(sprintf(mixFolder, type{1}));
end

for i = 1:2000
	m = randi(length(blend));

    for j = 1:length(types)
%         if ~exist(file, 'file')
%             fprintf('Error: file %s not exist', file);
%             file = sprintf(baseFolder, folder{1}, i); % TODO: Check why some files not rendered
%         end
        file = sprintf(baseFile, blend{m}, types{j}, i, exts{j});
        copyfile(file, sprintf(mixFile, types{j}, i, exts{j}));
    end
end