package com.wungong.jobservice.persistence;

import java.util.UUID;

import org.springframework.stereotype.Component;

import com.wungong.jobservice.model.Job;

@Component
public class JobRepositoryImpl implements JobRepository{

	@Override
	public UUID jobId() {
		// TODO Auto-generated method stub
		return UUID.randomUUID();
	}

	@Override
	public Job jobOfId(UUID jobId) {
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
