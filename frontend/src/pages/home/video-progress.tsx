import { useEffect, useState } from 'react';
import { DownloadJob } from '.';
import { Card, CardContent, CardMedia, LinearProgress, Typography } from '@mui/material';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';


export default function VideoProgress({ id, title, thumbnail }: DownloadJob) {
  const [progress, setProgress] = useState(0);
  const [status, setStatus] = useState('');
  const [isPolling, setIsPolling] = useState(false);


  const downloadFile = () => {
    fetch(`http://localhost:5000/yt/download?id=${id}`).then((res) => {
      res.json().then((data) => {
        if(data.url){
          const a = document.createElement('a');
          a.href = data.url;
          a.download = `${title}.mp3`;
          document.body.appendChild(a);
          a.click();
          a.remove();
        }
      });
    });
  };
  
  const pollDownload = () => {
    setIsPolling(true);
    fetch(`http://localhost:5000/yt/status?id=${id}`).then((res) => {
      if (res.status === 200) {
        if (res.headers.get('Content-Type') === 'application/json') {
          res.json().then((data) => {
            setProgress(data.progress);
            setStatus(data.status);
            if(data.status === 'finished'){
              downloadFile();
            }
          });
        }
      }
    }).finally(() => {
      setIsPolling(false);
    });
  };


  useEffect(() => {
    const interval = setInterval(() => {
      if(!isPolling && status !==  'finished'){
        pollDownload();
      }
    }, 500);
    return () => clearInterval(interval);
  }, [isPolling, status]);


  return (
    <Card sx={{ mt: 2 }}>
      <CardMedia
        component="img"
        height="140"
        width="140"
        image={thumbnail}
        alt={title}
      />
      <CardContent>
        <Typography variant="h5" component="div">
          {title}
          {status === 'finished' && <CheckCircleIcon color="success" sx={{ ml: 1 }} />}
        </Typography>
        <Typography variant="body2" color="text.secondary">
          Statut: {status}
        </Typography>
        <LinearProgress color={status === 'finished' ? 'success':'info'} variant="determinate" value={progress} />
      </CardContent>
    </Card>
  );
}