package com.wungong.jobservice.request;

import java.util.List;

import com.fasterxml.jackson.annotation.JsonProperty;
import com.wungong.jobservice.model.Address;
import com.wungong.jobservice.model.Benefits;
import com.wungong.jobservice.model.Compensation;
import com.wungong.jobservice.model.Duty;
import com.wungong.jobservice.model.Employer;
import com.wungong.jobservice.model.JobType;
import com.wungong.jobservice.model.Skill;

import lombok.Data;

@Data
public class CreateJobRequest {
	
	private JobType jobType;
	
	private String title;
	
	private String description;
	
	private Compensation compensation;
	
	private Benefits benefits;
	
	private Address location;
	
	private Employer employer;
	
	private List<Duty> duties;
	
	private List<Skill> requiredSkills;
	
	private List<Skill> preferedSkills;

}
