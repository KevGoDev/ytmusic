import React, { useEffect, useState } from 'react';
import { Container, TextField, Button, Box, LinearProgress, Typography, Stack, Grid } from '@mui/material';
import queryString from 'query-string';
import VideoProgress from './video-progress';


export type DownloadJob = {
  id: string;
  title: string;
  thumbnail: string;
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
    if (!playlist_id) {
      setErrorMsg("URL invalide");
      setIsDownloading(false);
      return;
    }
    // Create download jobs
    fetch(`http://localhost:5000/yt/convert?list=${playlist_id}`).then((res) => {
      if (res.status === 200) {
        res.json().then((data) => {
          setTrackedJobs(data.jobs);
        });
      } else {
        setErrorMsg("Erreur lors du téléchargement");
      }
    }).catch((err) => {
      setErrorMsg("Erreur lors du téléchargement");
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
      setErrorMsg("URL invalide");
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
        setErrorMsg("Erreur lors du téléchargement");
      }
    }).catch((err) => {
      setErrorMsg("Erreur lors du téléchargement");
    }).finally(() => {
      setIsDownloading(false);
    });
  };


  return (
    <Container>
      <Stack direction={"column"} spacing={2}>
        <div>
          <Typography variant="h4" align="center" gutterBottom>
            Convertisseur Youtube vers MP3
          </Typography>
          {errorMsg && <Box color="error.main" sx={{ pb: 2 }}>{errorMsg}</Box>}
          <TextField
            label="Lien Youtube"
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
                Télécharger la playlist
              </Button>
              <Button
                variant="contained"
                color="primary"
                onClick={handleDownload}
                disabled={isDownloading}
              >
                Télécharger vers MP3
              </Button>
            </Stack>
          </Box>
        </div>

        <Grid container spacing={2}>
          {trackedJobs.map((job) => (
            <Grid key={job.id} item xs={8} md={4}>
              <VideoProgress {...job} />
            </Grid>
          ))}
        </Grid>
      </Stack>
    </Container>
  );
}