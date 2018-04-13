package com.wungong.jobservice.model;

import java.util.List;
import java.util.UUID;

import com.datastax.driver.mapping.annotations.PartitionKey;
import com.datastax.driver.mapping.annotations.Table;

@Table(keyspace = "jobservice", name = "jobs")
public class Job {
	
	@PartitionKey
	private UUID jobId;
	
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
	
	public void setJobId(UUID jobId) {
		this.jobId = jobId;
	}

	public Job(UUID jobId){
		this.jobId = jobId;
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

	public UUID getJobId() {
		return jobId;
	}

}
