package com.wungong.jobservice.request;

import java.util.List;
import java.util.UUID;

import com.wungong.jobservice.model.Address;
import com.wungong.jobservice.model.Benefit;
import com.wungong.jobservice.model.Compensation;
import com.wungong.jobservice.model.Duty;
import com.wungong.jobservice.model.JobType;

public class CreateJobRequest {
	
	private JobType jobType;
	
	private String title;
	
	private String description;
	
	private Compensation compensation;
	
	private List<Benefit> benefits;
	
	private Address location;
	
	private UUID employerId;
	
	private List<Duty> duties;
	
	private List<UUID> requiredSkillIds;
	
	private List<UUID> preferedSkillIds;

	public CreateJobRequest(JobType jobType, String title, String description, Compensation compensation,
			List<Benefit> benefits, Address location, UUID employerId, List<Duty> duties, List<UUID> requiredSkills,
			List<UUID> preferedSkills) {
		this.jobType = jobType;
		this.title = title;
		this.description = description;
		this.compensation = compensation;
		this.benefits = benefits;
		this.location = location;
		this.employerId = employerId;
		this.duties = duties;
		this.requiredSkillIds = requiredSkills;
		this.preferedSkillIds = preferedSkills;
	}

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

	public List<Benefit> getBenefits() {
		return benefits;
	}

	public void setBenefits(List<Benefit> benefits) {
		this.benefits = benefits;
	}

	public Address getLocation() {
		return location;
	}

	public void setLocation(Address location) {
		this.location = location;
	}

	public UUID getEmployerId() {
		return employerId;
	}

	public void setEmployerId(UUID employerId) {
		this.employerId = employerId;
	}

	public List<Duty> getDuties() {
		return duties;
	}

	public void setDuties(List<Duty> duties) {
		this.duties = duties;
	}

	public List<UUID> getRequiredSkillIds() {
		return requiredSkillIds;
	}

	public void setRequiredSkillIds(List<UUID> requiredSkillIds) {
		this.requiredSkillIds = requiredSkillIds;
	}

	public List<UUID> getPreferedSkillIds() {
		return preferedSkillIds;
	}

	public void setPreferedSkillIds(List<UUID> preferedSkillIds) {
		this.preferedSkillIds = preferedSkillIds;
	}

}
