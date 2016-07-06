package com.wungong.jobservice.request;

import java.util.List;

import com.fasterxml.jackson.annotation.JsonProperty;
import com.wungong.jobservice.model.Benefits;
import com.wungong.jobservice.model.Compensation;
import com.wungong.jobservice.model.Duty;
import com.wungong.jobservice.model.Employer;
import com.wungong.jobservice.model.JobType;
import com.wungong.jobservice.model.Location;
import com.wungong.jobservice.model.Skill;

public class CreateJobRequest {
	
	@JsonProperty
	private JobType jobType;
	
	@JsonProperty
	private String title;
	
	@JsonProperty
	private String description;
	
	@JsonProperty
	private Compensation compensation;
	
	@JsonProperty
	private Benefits benefits;
	
	@JsonProperty
	private Location location;
	
	@JsonProperty
	private Employer employer;
	
	@JsonProperty
	private List<Duty> duties;
	
	@JsonProperty
	private List<Skill> requiredSkills;
	
	@JsonProperty
	private List<Skill> preferedSkills;

	public JobType getJobType() {
		return jobType;
	}

	public void setJobType(JobType jobType) {
		this.jobType = jobType;
	}

	public String getTitle() {
		return title;
	}

	public void setTitle(String title) {
		this.title = title;
	}

	public String getDescription() {
		return description;
	}

	public void setDescription(String description) {
		this.description = description;
	}

	public Compensation getCompensation() {
		return compensation;
	}

	public void setCompensation(Compensation compensation) {
		this.compensation = compensation;
	}

	public Benefits getBenefits() {
		return benefits;
	}

	public void setBenefits(Benefits benefits) {
		this.benefits = benefits;
	}

	public Location getLocation() {
		return location;
	}

	public void setLocation(Location location) {
		this.location = location;
	}

	public Employer getEmployer() {
		return employer;
	}

	public void setEmployer(Employer employer) {
		this.employer = employer;
	}

	public List<Duty> getDuties() {
		return duties;
	}

	public void setDuties(List<Duty> duties) {
		this.duties = duties;
	}

	public List<Skill> getRequiredSkills() {
		return requiredSkills;
	}

	public void setRequiredSkills(List<Skill> requiredSkills) {
		this.requiredSkills = requiredSkills;
	}

	public List<Skill> getPreferedSkills() {
		return preferedSkills;
	}

	public void setPreferedSkills(List<Skill> preferedSkills) {
		this.preferedSkills = preferedSkills;
	}


}
