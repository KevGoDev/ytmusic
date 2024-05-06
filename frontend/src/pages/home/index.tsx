import React, { useEffect, useState } from 'react';
import { Container, TextField, Button, Box, LinearProgress, Typography } from '@mui/material';
import queryString from 'query-string';

export default function DownloadPage() {
  const [url, setUrl] = useState('');
  const [videoId, setVideoId] = useState<string | null>(null);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);
  const handleUrlChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setUrl(event.target.value);
  };

  // const pollDownload = () => {
  //   if(videoId === null) return;    
  //   fetch(`http://localhost:5000/yt/download?id=${videoId}`).then((res) => {
  //     if (res.status === 200) {
  //       if(res.headers.get('Content-Type') === 'application/json') {
  //         // Show progress
  //         res.json().then((data) => {
  //           console.log(data);
  //         });
  //       }
  //       else{
  //         // Downloaded, let's not download again
  //         setVideoId(null);
  //       }
  //     } 
  //   });
  // }


  const handleDownload = () => {
    setErrorMsg(null);
    const params = url.split('?')[1];
    const video_id = queryString.parse(params).v;
    if (!video_id) {
      setErrorMsg("URL invalide");
      setVideoId(null);
      return;
    }
    setVideoId(video_id as string); 
    fetch(`http://localhost:5000/yt/convert?id=${video_id}`).then((res) => {
      if (res.status === 200) {
        res.blob().then((blob) => {
          const url = window.URL.createObjectURL(blob);
          const a = document.createElement('a');
          a.href = url;
          const contentDisposition = res.headers.get('content-disposition');
          let filename = 'audio.mp3'; // Default filename if not found
          if (contentDisposition) {
            const filenameRegex = /filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/;
            const matches = filenameRegex.exec(contentDisposition);
            if (matches != null && matches[1]) {
              filename = matches[1].replace(/['"]/g, '');
            }
          }
          a.download = filename;
          document.body.appendChild(a);
          a.click();
          a.remove();
          window.URL.revokeObjectURL(url);
          setVideoId(null);
        });
      } else {
        setErrorMsg("Erreur lors du téléchargement");
      }
    }).catch((err) => {
      setErrorMsg("Erreur lors du téléchargement");
    });
  };


  // useEffect(() => { 
  //   const interval = setInterval(() => {
  //     pollDownload();
  //   }, 500);
  //   return () => clearInterval(interval);
  // }, []);


  return (
    <Container sx={{ pt: '15%' }}>
      <Typography variant="h4" align="center" gutterBottom>
        Convertisseur Youtube vers MP3
      </Typography>
      {errorMsg && <Box color="error.main" sx={{pb:2}}>{errorMsg}</Box>}
      <TextField
        label="Lien Youtube"
        variant="outlined"
        value={url}
        onChange={handleUrlChange}
        fullWidth
      />
      <Box display="flex" justifyContent="center" mt={2}>
        <Button
          variant="contained"
          color="primary"
          onClick={handleDownload}
          disabled={videoId !== null}
        >
          Telecharger vers MP3
        </Button>
      </Box>
      {videoId !== null && <LinearProgress sx={{ mt: 2 }} value={0.5}/>}
    </Container>
  );
}