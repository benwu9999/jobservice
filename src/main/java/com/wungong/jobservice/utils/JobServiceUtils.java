package com.wungong.jobservice.utils;

import java.util.UUID;

import org.springframework.stereotype.Component;

import com.wungong.jobservice.model.Job;
import com.wungong.jobservice.request.CreateJobRequest;
import com.wungong.jobservice.request.UpdateJobRequest;

@Component
public class JobServiceUtils {

	public Job convertToJob(UUID jobId, CreateJobRequest request) {
		Job job = new Job(jobId);
		setJobValues(request, job);
		return job;
	}
	
	public Job updateJob(Job jobToUpdate, UpdateJobRequest request) {
		setJobValues(request, jobToUpdate);
		return jobToUpdate;
	}

	private void setJobValues(CreateJobRequest request, Job job) {
		job.setBenefits(request.getBenefits());
		job.setCompensation(request.getCompensation());
		job.setDescription(request.getDescription());
		job.setDuties(request.getDuties());
		job.setEmployerId(request.getEmployerId());
		job.setJobType(request.getJobType());
		job.setLocation(request.getLocation());
		job.setPreferedSkills(request.getPreferedSkills());
		job.setRequiredSkills(request.getRequiredSkills());
		job.setTitle(request.getTitle());
	}

}
