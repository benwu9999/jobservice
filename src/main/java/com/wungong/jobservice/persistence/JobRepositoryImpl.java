package com.wungong.jobservice.persistence;

import java.util.UUID;

import com.wungong.jobservice.model.Job;
import com.wungong.jobservice.model.JobId;

public class JobRepositoryImpl implements JobRepository{

	@Override
	public JobId jobId() {
		// TODO Auto-generated method stub
		return new JobId(UUID.randomUUID());
	}

	@Override
	public Job jobOfId(JobId jobId) {
		// TODO Auto-generated method stub
		return null;
	}

	@Override
	public Boolean remove(Job jobToDelete) {
		// TODO Auto-generated method stub
		return null;
	}

	@Override
	public void add(Job convertToJob) {
		// TODO Auto-generated method stub
		
	}

}
