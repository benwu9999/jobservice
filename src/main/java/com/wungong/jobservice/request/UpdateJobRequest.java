package com.wungong.jobservice.request;

import java.util.List;
import java.util.UUID;

import com.wungong.jobservice.model.Address;
import com.wungong.jobservice.model.Benefit;
import com.wungong.jobservice.model.Compensation;
import com.wungong.jobservice.model.Duty;
import com.wungong.jobservice.model.JobType;

public class UpdateJobRequest extends CreateJobRequest{
	
	final private String jobId;

	public UpdateJobRequest(JobType jobType, String title, String description, Compensation compensation,
			List<Benefit> benefits, Address location, UUID employerId, List<Duty> duties, List<UUID> requiredSkills,
			List<UUID> preferedSkills, String jobId) {
		super(jobType, title, description, compensation, benefits, location, employerId, duties, requiredSkills,
				preferedSkills);
		this.jobId = jobId;
	}

	public String getJobId() {
		return jobId;
	}

}
