function [X, Y] = read_joint_info(jointFile)
    T = readtable(jointFile, 'ReadVariableNames', false);
    
    % map the order of the annotation
    map = [7, 2, 4, 3, 1, 6, 9, 11, 13, 12, 10, 8, 14, 5];
    X = T.Var2(map);
    Y = T.Var3(map);
end

