import React, { useEffect, useState } from 'react';
import { Container, TextField, Button, Box, LinearProgress, Typography, Stack, Grid } from '@mui/material';
import queryString from 'query-string';
import VideoProgress from './video-progress';


export type DownloadJob = {
  id: string;
  title: string;
  thumbnail: string;
  completed: boolean;
};

export default function DownloadPage() {
  const [url, setUrl] = useState('');
  const [errorMsg, setErrorMsg] = useState<string | null>(null);
  const [isDownloading, setIsDownloading] = useState(false);
  const [trackedJobs, setTrackedJobs] = useState<DownloadJob[]>([]);
  const handleUrlChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setUrl(event.target.value);
  };


  const handleDownloadPlaylist = () => {
    setIsDownloading(true);
    setErrorMsg(null);
    const params = url.split('?')[1];
    const playlist_id = queryString.parse(params).list;
    const video_id = queryString.parse(params).v;
    if (!playlist_id) {
      setErrorMsg("URL invalide");
      setIsDownloading(false);
      return;
    }
    // Create download jobs
    let cv_url = `http://localhost:5000/yt/convert?list=${playlist_id}`;
    if (video_id) {
      cv_url += `&id=${video_id}`;
    }
    fetch(cv_url).then((res) => {
      if (res.status === 200) {
        res.json().then((data) => {
          let jobs = data.jobs;
          for (let i = 0; i < jobs.length; i++) {
            jobs[i].completed = false;
          }
          setTrackedJobs(jobs);
        });
      } else {
        setErrorMsg("Error while downloading");
      }
    }).catch((err) => {
      setErrorMsg("Error while downloading, playlist invalid or private");
    }).finally(() => {
      setIsDownloading(false);
    });
  };


  const handleDownload = () => {
    setIsDownloading(true);
    setErrorMsg(null);
    setTrackedJobs([]);
    const params = url.split('?')[1];
    const video_id = queryString.parse(params).v;
    if (!video_id) {
      setErrorMsg("Invalid URL");
      setIsDownloading(false);
      return;
    }
    // Create download jobs
    fetch(`http://localhost:5000/yt/convert?id=${video_id}`).then((res) => {
      if (res.status === 200) {
        res.json().then((data) => {
          setTrackedJobs(data.jobs);
        });
      } else {
        setErrorMsg("Error while downloading");
      }
    }).catch((err) => {
      setErrorMsg("Error while downloading");
    }).finally(() => {
      setIsDownloading(false);
    });
  };

  const setCompleted = (id: string) => {
    setTrackedJobs((jobs) => {
      return jobs.map((job) => {
        if (job.id === id) {
          job.completed = true;
        }
        return job;
      });
    });
  }

  const getCompletedCount = () => {
    return trackedJobs.filter((job) => job.completed).length;
  }


  return (
    <Container>
      <Stack direction={"column"} spacing={2}>
        <div>
          <Typography variant="h4" align="center" gutterBottom>
            Youtube to MP3
          </Typography>
          {errorMsg && <Box color="error.main" sx={{ pb: 2 }}>{errorMsg}</Box>}
          <TextField
            label="Youtube URL"
            variant="outlined"
            value={url}
            onChange={handleUrlChange}
            fullWidth
          />
          <Box display="flex" justifyContent="center" mt={2}>
            <Stack spacing={2} direction="row">
              <Button
                variant="contained"
                color="primary"
                onClick={handleDownloadPlaylist}
                disabled={isDownloading || !url.includes('list=')}
              >
                Download playlist
              </Button>
              <Button
                variant="contained"
                color="primary"
                onClick={handleDownload}
                disabled={isDownloading}
              >
                Convert to MP3
              </Button>
            </Stack>
          </Box>
        </div>

        {trackedJobs.length > 0 && (
          <Box>
            <Typography variant="h5" align="center" gutterBottom>
              Downloading ({getCompletedCount()}/{trackedJobs.length})
            </Typography>
            <LinearProgress variant='determinate' value={getCompletedCount()/trackedJobs.length*100} />
            <Grid container spacing={2}>
              {trackedJobs.map((job) => (
                <Grid key={job.id} item xs={8} md={4}>
                  <VideoProgress {...job} setCompleted={setCompleted} />
                </Grid>
              ))}
            </Grid>
          </Box>
        )}
      </Stack>
    </Container>
  );
}