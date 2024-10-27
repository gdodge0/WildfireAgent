import axios from "axios"

export async function fetchFireItems(){
  try {
    const response = await axios.get('/api/v1/get_fire_info')
    return response.data
  } catch (err) {
      console.log(err)
      console.log('Failed to fetch fire information')
  }
}

export async function fetchBatchLatestNews(fires) {
    let fire_ids = []
      fires.forEach((fire) => {
        fire_ids.push(fire.id)
      })
    try {
    const response =
        await axios.get('/api/v1/get_latest_news_batch', {
            params: {
                fire_ids: fire_ids // fire_ids should be an array like [36560, 36643, 36623]
            },
            paramsSerializer: params => {
                return Object.keys(params)
                    .map(key => params[key].map(id => `${key}=${id}`).join('&'))
                    .join('&');
            }
        })
        return response.data
  } catch (err) {
      console.log(err)
      console.log('Failed to fetch latest news')
  }
}
