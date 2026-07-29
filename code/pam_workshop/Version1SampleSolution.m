close all, clear, clc
%Suppose you tested N=12 subjects
Nsubj=12;
% First, for each subject you perform a psychological test for some
% personality trait. Let's call their test score T.
% To simulate this, assign a score to each subject, drawn
% at random from a normal distribution with a mean of mT and a standard
% deviation of sT. 
mT=50; sT=10;
T=sT*randn(Nsubj,1)+mT; 
%not specified in instructions, but I'm going to make T an integer
T=round(T);

% Then for each subject simulate an fMRI brain scan... The differential
% activity is measured separately in each of Nvox voxels. 
% Although in real data these would be organized in a 3D volume, we can
% just make a 1D vector of the voxels.
Nvox=5000; 
% Simulate that 10% of the voxels really are affected
Naffected=round(0.1*Nvox);
TaskDependentVoxels=1:Naffected; %doesn't matter which ones 
TaskIndependentVoxels=Naffected+1:Nvox;

%% simulate the values of task dependent voxels by drawing from a normal
% distribution with mean=mA std=sA.
mA=1; sA=1;
DA(1:Nsubj,TaskDependentVoxels)=...
    sA*randn(Nsubj,length(TaskDependentVoxels))+mA;

% Assume the rest of the voxels have no difference in activity on average
% (“task independent” voxels). Simulate their values by drawing from a
% normal distribution with mean=0 std=sA
DA(1:Nsubj,TaskIndependentVoxels)= ...
    sA*randn(Nsubj,length(TaskIndependentVoxels));
  
% Question 1: Replicate the described data analysis workflow:
% 1. Find out how correlated the Differential Activity in each voxel is
% with the subjects’ psychology test scores
[r p]=corr(DA,T);%Nvox r and p values, r ranges -1 to 1, p ranges 0 -1 

% 2. Define the “Relevant” voxels to be all voxels that are correlated with
% the psychology test with a positive correlation r>0.1 with a statistical
% significance p<0.05
ModulatedVoxels=find(r>0.1 & p<.05);  
   
% 3. Within each subject, average the Differential Activity of the
% “Relevant” voxels to get a single “Relevant Brain Network Activity” value
% for each subject.
RBNA=mean(DA(:,ModulatedVoxels)');%averages within subject over selected voxels
%check my work: I should now have 12 numbers:   size(RBNA)

% 4. Make a scatter plot of the Relevant Brain Network Activity in a
% subject versus their psychology test result (1 symbol per subject, 12
% subjects).
subplot(221),hold off
plot(RBNA,T,'bo','markerfacecolor','b');
ax=axis; axis(ax); lsline %plot the best fit line
set(gca,'fontsize',12)
xlabel('Relevant Brain Network Activity'),ylabel('Pysch Test Score')
title('Standard Analysis Method, No Real Effect')

%determine the R^2 abd P value of the correlation.
[r_model p_model]=corr(RBNA',T);
Rsquared=r_model^2;

%Print R^2 and P values somewhere on your plot
%this code is to find a good location on the plot
xlims=get(gca,'xlim'); xpos=min(xlims)+0.05*range(xlims);
ylims=get(gca,'ylim'); ypos=max(ylims)-0.05*range(ylims);
text(xpos,ypos,sprintf('R^2=%.4f P=%.2e',Rsquared,p_model))

 
%% Question 2 Repeat the entire simulation above, but this time simulate
% that the outcome of the psychology test really does predict something...
% to achieve this, instead of using the same mean=m for the task-dependent
% voxels when you simulate the differential activity, set the mean in
% responsive voxels to be some function of T

% Here we made a scaled, shifted version of T with mean mA and std=k*sA
% k determines how big the psychology-trait effect is relative to noise
%  k=1 the task-related signal will be mostly determined by the trait
%  k=0.1 the task-related signal will be weakly affected by trait
k=0.2;%  correlation between task-related signal and trait is modest
Tscaled=(k*sA/std(T))*(T-mean(T))+mA;
% and then set the task-dependent activity of each subject to Tscaled+noise
clear DA_real
for i=1:Nsubj 
    DA_real(i,TaskDependentVoxels)=sA*randn(1,length(TaskDependentVoxels))+Tscaled(i);
end
% Assume the rest of the voxels have no difference in activity 
DA_real(1:Nsubj,TaskIndependentVoxels)=sA*randn(Nsubj,length(TaskIndependentVoxels));

% Find out how correlated the Differential Activity in each voxel is
% with the subjects’ psychology test scores
[r p]=corr(DA_real,T);%Nvox r and p values, r ranges -1 to 1, p ranges 0 -1 
ModulatedVoxels=find(r>0.1 & p<.05);  
 
RBNA_real=mean(DA_real(:,ModulatedVoxels)');%averages within subject over selected voxels
%check my work: I should now have 12 numbers   size(RBNA)

subplot(222),hold off
plot(RBNA_real,T,'bo','markerfacecolor','b');
ax=axis; axis(ax); lsline %plot the best fit line
set(gca,'fontsize',12)
xlabel('Relevant Brain Network Activity'),ylabel('Pysch Test Score')
title('Standard Analysis Method, With Real Effect')

%determine the R^2 abd P value of the correlation.
[r_model p_model]=corr(RBNA_real',T);
Rsquared=r_model^2;

%Print R^2 and P values somewhere on your plot
%this code is to find a good location on the plot
xlims=get(gca,'xlim'); xpos=min(xlims)+0.05*range(xlims);
ylims=get(gca,'ylim'); ypos=max(ylims)-0.05*range(ylims);
text(xpos,ypos,sprintf('R^2=%.4f P=%.2e',Rsquared,p_model))


