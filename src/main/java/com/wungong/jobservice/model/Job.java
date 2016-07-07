package com.wungong.jobservice.model;

import java.util.List;
import java.util.UUID;

import lombok.Data;

@Data
public class Job {
	
	final private UUID jobId;
	
	private JobType jobType;
	
	private String title;
	
	private String description;
	
	private Compensation compensation;
	
	private List<Benefit> benefits;
	
	private Address location;
	
	private UUID employerId;
	
	private List<Duty> duties;
	
	private List<Skill> requiredSkills;
	
	private List<Skill> preferedSkills;

}
