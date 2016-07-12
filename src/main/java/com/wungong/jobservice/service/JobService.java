package com.wungong.jobservice.service;

import java.util.UUID;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

import com.wungong.jobservice.model.Job;
import com.wungong.jobservice.persistence.JobRepository;
import com.wungong.jobservice.request.CreateJobRequest;
import com.wungong.jobservice.request.UpdateJobRequest;
import com.wungong.jobservice.utils.JobServiceUtils;

@Component
public class JobService {
	
	private final Logger log = LoggerFactory.getLogger(this.getClass());
	
	@Autowired
	JobRepository jobRepository;
	
	@Autowired
	JobServiceUtils utils;

	public void createJob(CreateJobRequest request) {
		UUID jobId = jobRepository.jobId();
		jobRepository.add(utils.convertToJob(jobId, request));
		log.info("added job with jobId " + jobId);
	}
	
	public void deleteJob(String id) {
		UUID jobId = UUID.fromString(id);
		Job jobToDelete = jobRepository.jobOfId(jobId);
		if(jobToDelete != null && jobRepository.remove(jobToDelete))
			log.info("removed job with jobId " + jobId);
		else
			log.debug("job with jobId does not exist: " + jobId);
	}
	
	public void updateJob(UpdateJobRequest request) {
		UUID jobId = UUID.fromString(request.getJobId());
		Job jobToUpdate = jobRepository.jobOfId(jobId);
		jobRepository.add(utils.updateJob(jobToUpdate, request));
		log.info("updated job with jobId " + jobId);
	}

	public Job getJob(String id) {
		UUID jobId = UUID.fromString(id);
		Job job = jobRepository.jobOfId(jobId);
		log.info("retrieved job with jobId " + jobId);
		return job;
	}

}
