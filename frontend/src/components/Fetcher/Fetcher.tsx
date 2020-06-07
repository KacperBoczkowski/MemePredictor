import { useState, useEffect } from 'react'
import axios from 'axios'

interface IFetcher {
  url: string,
  page: number
}

interface IDataItem {
  id: string,
  author: string
}

const useFetcher = ({ url, page }: IFetcher) => {
  const [data, setData] = useState<IDataItem[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const [hasMore, setHasMore] = useState(true)

  useEffect(() => {
    const fetchData = async ({ url, page }: IFetcher) => {
      setLoading(true)

      try {
        const response = await axios({ method: 'GET', url, params: { page, limit: 10 } })

        setData((prevData) => [...prevData, ...response.data])
        setHasMore(response.data.length > 0)
      } catch (e) {
        setError(e)
      } finally {
        setLoading(false)
      }
    }

    fetchData({ url, page })
  }, [url, page])

  return { data, loading, error, hasMore }
}

export default useFetcher
