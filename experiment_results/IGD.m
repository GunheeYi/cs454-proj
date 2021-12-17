% Code obtained from
% https://www.mathworks.com/matlabcentral/mlc-downloads/downloads/5abeaa45-8990-423b-a3b4-808e2ade1974/6a4aff9a-a914-47f4-96b9-51734fab7ba9/previews/Indicator_calculation/IGD_calculation.m/index.html

function  result=IGD(obtained_ps,reference_ps)
% IGD_calculation: Calculate the IGD of the obtained Pareto set
% Dimension: n_var --- dimensions of decision space

%% Input:
%                      Dimension                                                   Description
%      obtained_ps     population_size x n_var                                     Obtained Pareto set     
%      reference_ps    num_of_solutions_in_reference_ps x n_var                    Reference Pareto set

%% Output:
%                     Description
%      IGD            Inverted Generational Distance (IGD) of the obtained Pareto set

n_ref=size(reference_ps,1);

for i=1:n_ref
    ref_m=repmat(reference_ps(i,:),size(obtained_ps,1),1); 
    d=obtained_ps-ref_m;    %Calculate the the differences btween the obtained_ps and the reference_ps
    D=sum(abs(d).^2,2).^0.5;%Calculate the the distance btween the obtained_ps and the reference_ps
    obtained_to_ref(i)=min(D);
end
result=sum(obtained_to_ref)/n_ref;
end