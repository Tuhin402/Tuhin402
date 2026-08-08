class GitHubQueries:
    """
    Collection of reusable GraphQL queries.
    """

    # --------------------------------------------------

    VIEWER_PROFILE = """
    query {

      viewer {
        login
        name
        bio
        avatarUrl
        followers {
          totalCount
        }
        following {
          totalCount
        }
      }

    }
    """

    # --------------------------------------------------

    REPOSITORIES = """
    query {

      viewer {

        repositories(

          first:100,
          ownerAffiliations:OWNER,
          isFork:false,

          orderBy:{
            field:UPDATED_AT,
            direction:DESC
          }

        ){

          nodes{

            name
            description
            stargazerCount
            forkCount
            url
            languages(
              first:10,
              orderBy:{
                field:SIZE,
                direction:DESC
              }

            ){

              edges{
                size
                node{
                  name
                }

              }

            }

          }

        }

      }

    }
    """

    # --------------------------------------------------

    CONTRIBUTIONS = """
    query {

      viewer {

        contributionsCollection {
          contributionCalendar {
            totalContributions
            weeks {
              contributionDays {
                contributionCount
                contributionLevel
                date
              }
            }
          }
        }
      }
    }
    """