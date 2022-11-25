use crate::error::Error;
use std::fs::read_to_string;
use std::path::Path;
use std::result::Result;
use std::time::Duration;
use std::time::Instant;

const MINIMUM_TIME_BETWEEN_DOWNLOADS: Duration = Duration::from_secs(3);

#[derive(Debug, Default)]
pub struct Inputs {
    session_token: Option<String>,
    last_download_time: Option<Instant>,
}

impl Inputs {
    pub fn new() -> Inputs {
        Default::default()
    }

    pub fn get(&mut self, year: u32, day: u32) -> Result<String, Error> {
        let path = format!("data/{year}/{day:0>2}.txt");
        let path = Path::new(&path);
        if let Ok(input) = std::fs::read_to_string(path) {
            return Ok(input);
        }

        let input = self.download(year, day)?;
        std::fs::create_dir_all(path.parent().unwrap())?;
        std::fs::write(path, &input)?;
        Ok(input)
    }

    fn get_session_token(&mut self) -> Result<&str, Error> {
        if self.session_token.is_none() {
            self.session_token = Some(read_to_string("./session_token.txt")?);
        }
        Ok(self.session_token.as_ref().unwrap())
    }

    fn download(&mut self, year: u32, day: u32) -> Result<String, Error> {
        let session_token = self.get_session_token()?;
        let cookie = format!("session={session_token}");

        let now = Instant::now();
        if let Some(last) = self.last_download_time {
            let delta = now - last;
            if delta < MINIMUM_TIME_BETWEEN_DOWNLOADS {
                std::thread::sleep(MINIMUM_TIME_BETWEEN_DOWNLOADS - delta);
            }
        };
        self.last_download_time = Some(now);
        let response = ureq::get(&format!("https://adventofcode.com/{year}/day/{day}/input"))
            .set("cookie", &cookie)
            .timeout(Duration::from_secs(5))
            .call()
            .map_err(Box::new)?;

        let mut buf = String::new();
        response.into_reader().read_to_string(&mut buf)?;
        Ok(buf)
    }
}
