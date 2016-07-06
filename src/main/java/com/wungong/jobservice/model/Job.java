package com.wungong.jobservice.model;

import java.util.List;

import lombok.Data;

@Data
public class Job {
	
	final private JobId id;
	
	private JobType jobType;
	
	private String title;
	
	private String description;
	
	private Compensation compensation;
	
	private Benefits benefits;
	
	private Location location;
	
	private Employer employer;
	
	private List<Duty> duties;
	
	private List<Skill> requiredSkills;
	
	private List<Skill> preferedSkills;

}
